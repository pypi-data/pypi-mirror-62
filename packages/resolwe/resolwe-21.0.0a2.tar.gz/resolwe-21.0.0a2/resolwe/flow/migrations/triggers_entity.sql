-- Trigger after insert/update Entity object.
CREATE OR REPLACE FUNCTION generate_resolwe_entity_search(entity_line flow_entity)
    RETURNS tsvector
    LANGUAGE plpgsql
    AS $$
    DECLARE
        search tsvector;
    BEGIN
        WITH owners AS (
            SELECT
                object_pk::int entity_id,
                array_to_string(array_agg(username), ' ') AS usernames,
                array_to_string(array_remove(array_agg(first_name), ''), ' ') AS first_names,
                array_to_string(array_remove(array_agg(last_name), ''), ' ') AS last_names
            FROM auth_user
            JOIN guardian_userobjectpermission ON auth_user.id=guardian_userobjectpermission.user_id
            WHERE
                content_type_id=(SELECT id FROM django_content_type WHERE app_label='flow' and model='entity')
                AND permission_id=(SELECT id FROM auth_permission WHERE codename='owner_entity')
                AND object_pk::int=entity_line.id
            GROUP BY object_pk
        )
        SELECT
            -- Entity name.
            setweight(to_tsvector('simple', entity.name), 'A') ||
            setweight(edge_ngrams(entity.name), 'B') ||
            setweight(edge_ngrams(get_characters(entity.name)), 'B') ||
            setweight(edge_ngrams(get_numbers(entity.name)), 'B') ||
            -- Collection description.
            setweight(to_tsvector('simple', entity.description), 'B') ||
            -- Contributor username.
            setweight(to_tsvector('simple', contributor.username), 'B') ||
            setweight(edge_ngrams(contributor.username), 'C') ||
            setweight(edge_ngrams(get_characters(contributor.username)), 'C') ||
            setweight(edge_ngrams(get_numbers(contributor.username)), 'C') ||
            -- Contributor first name.
            setweight(to_tsvector('simple', contributor.first_name), 'B') ||
            setweight(edge_ngrams(contributor.first_name), 'C') ||
            -- Contributor last name.
            setweight(to_tsvector('simple', contributor.last_name), 'B') ||
            setweight(edge_ngrams(contributor.last_name), 'C') ||
            -- Owners usernames.
            setweight(to_tsvector('simple', owners.usernames), 'A') ||
            setweight(edge_ngrams(owners.usernames), 'B') ||
            setweight(edge_ngrams(get_characters(owners.usernames)), 'B') ||
            setweight(edge_ngrams(get_numbers(owners.usernames)), 'B') ||
            -- Owners first names.
            setweight(to_tsvector('simple', owners.first_names), 'A') ||
            setweight(edge_ngrams(owners.first_names), 'B') ||
            -- Owners last names.
            setweight(to_tsvector('simple', owners.last_names), 'A') ||
            setweight(edge_ngrams(owners.last_names), 'B') ||
            -- Entity tags.
            setweight(to_tsvector('simple', array_to_string(entity.tags, ' ')), 'B')
        FROM flow_entity entity
        JOIN owners ON entity.id=owners.entity_id
        JOIN auth_user contributor ON entity.contributor_id=contributor.id
        WHERE entity.id=entity_line.id
        INTO search;

        RETURN search;
    END;
    $$;

CREATE OR REPLACE FUNCTION entity_biut()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        SELECT generate_resolwe_entity_search(NEW) INTO NEW.search;

        RETURN NEW;
    END;
    $$;

CREATE TRIGGER entity_biut
    BEFORE INSERT OR UPDATE
    ON flow_entity
    FOR EACH ROW EXECUTE PROCEDURE entity_biut();


-- Trigger after update/insert/delete user permission object.
CREATE OR REPLACE FUNCTION handle_userpermission_entity(perm guardian_userobjectpermission)
    RETURNS void
    LANGUAGE plpgsql
    AS $$
    DECLARE
        entity_content_type_id int;
        owner_entity_permission_id int;
    BEGIN
        SELECT id FROM django_content_type WHERE app_label='flow' and model='entity' INTO entity_content_type_id;
        SELECT id FROM auth_permission WHERE codename='owner_entity' INTO owner_entity_permission_id;

        IF perm.content_type_id=entity_content_type_id AND perm.permission_id=owner_entity_permission_id THEN
            -- Set the search field to NULL to trigger entity_biut.
            UPDATE flow_entity SET search=NULL WHERE id=perm.object_pk::int;
        END IF;
    END;
    $$;

CREATE OR REPLACE FUNCTION userpermission_entity_aiut()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        perform handle_userpermission_entity(NEW);
        RETURN NEW;
    END;
    $$;

CREATE TRIGGER userpermission_entity_aiut
    AFTER INSERT OR UPDATE
    ON guardian_userobjectpermission
    FOR EACH ROW EXECUTE PROCEDURE userpermission_entity_aiut();

CREATE OR REPLACE FUNCTION userpermission_entity_adt()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        perform handle_userpermission_entity(OLD);
        RETURN OLD;
    END;
    $$;

CREATE TRIGGER userpermission_entity_adt
    AFTER DELETE
    ON guardian_userobjectpermission
    FOR EACH ROW EXECUTE PROCEDURE userpermission_entity_adt();


-- Trigger after update contributor.
CREATE OR REPLACE FUNCTION entity_contributor_aut()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        -- Set the search field to NULL to trigger entity_biut.
        UPDATE flow_entity SET search=NULL WHERE flow_entity.contributor_id=NEW.id;

        RETURN NEW;
    END;
    $$;

CREATE TRIGGER entity_contributor_aut
    AFTER UPDATE
    ON auth_user
    FOR EACH ROW EXECUTE PROCEDURE entity_contributor_aut();


-- Trigger after update owner.
CREATE OR REPLACE FUNCTION entity_owner_aut()
    RETURNS TRIGGER
    LANGUAGE plpgsql
    AS $$
    BEGIN
        WITH owner_permission AS (
            SELECT object_pk::int entity_id
            FROM guardian_userobjectpermission
            WHERE
                user_id=NEW.id
                AND content_type_id=(SELECT id FROM django_content_type WHERE app_label='flow' and model='entity')
                AND permission_id=(SELECT id FROM auth_permission WHERE codename='owner_entity')
        )
        -- Set the search field to NULL to trigger entity_biut.
        UPDATE flow_entity entity
        SET search=NULL
        FROM owner_permission perm
        WHERE entity.id=perm.entity_id;

        RETURN NEW;
    END;
    $$;

CREATE TRIGGER entity_owner_aut
    AFTER UPDATE
    ON auth_user
    FOR EACH ROW EXECUTE PROCEDURE entity_owner_aut();
