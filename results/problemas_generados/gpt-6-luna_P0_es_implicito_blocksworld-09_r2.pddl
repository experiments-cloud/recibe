(define (problem bloques)
  (:domain BLOCKS)
  (:objects
    a - block
    b - block
    c - block
    d - block
    e - block
    f - block
    g - block
    h - block
    i - block
  )
  (:init
    (ontable b)
    (ontable c)
    (on h b)
    (on d h)
    (on i d)
    (on a i)
    (on e a)
    (on g e)
    (on f g)
    (clear c)
    (clear f)
    (handempty)
  )
  (:goal
    (and
      (on g d)
      (on d b)
      (on b c)
      (on c a)
      (on a i)
      (on i f)
      (on f e)
      (on e h)
    )
  )
)
